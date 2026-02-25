from typing import Any, Literal, TypedDict
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.boards import Board
from src.models.elements import Element, ElementKind
from src.database import get_db
from src.models.users import User
from src.core.security import decode_access_token

router = APIRouter()


# TODO: Swap with Redis
rooms: dict[UUID, set[WebSocket]] = {}


async def get_current_user_ws(
    websocket: WebSocket, db: Session = Depends(get_db)
) -> User:
    auth = websocket.headers.get("authorization")
    token = None

    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    else:
        token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect()

    try:
        payload = decode_access_token(token)
        user_uuid = payload.get("uuid")
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect()

    if not user_uuid:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect()

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect()

    return user


async def broadcast(board_id: UUID, payload: Any, exclude: WebSocket | None = None):
    for ws in list(rooms.get(board_id, set())):
        if exclude is ws:
            continue
        try:
            await ws.send_json(payload)
        except Exception:
            rooms[board_id].discard(ws)


class ElementAdded(TypedDict):
    type: Literal["element_added"]
    element: dict[str, Any]


class ElementUpdated(TypedDict):
    type: Literal["element_updated"]
    element_id: UUID
    properties: dict[str, Any]


class ElementDeleted(TypedDict):
    type: Literal["element_deleted"]
    element_id: UUID


class CursorMoved(TypedDict):
    type: Literal["cursor_moved"]
    x: float
    y: float


# {
#   "type": "element_added",
#   "element": {
#     "type": "rectangle",
#     "properties": {
#       "x": 100,
#       "y": 100,
#       "width": 200,
#       "height": 150,
#       "color": "#000000",
#       "strokeWidth": 2
#     }
#   }
# }
async def cmd_add_element(
    board_id: UUID, cmd: ElementAdded, ws: WebSocket, user: User, db: Session
) -> dict[str, Any]:
    board = db.query(Board).filter_by(id=board_id, user_id=user.id).first()
    if not board:
        return {"type": "error", "detail": "board not found"}

    raw_kind = cmd["element"]["type"]
    try:
        kind = ElementKind(raw_kind)
    except ValueError:
        return {"type": "error", "detail": f"invalid element type: {raw_kind}"}

    new_element = Element(
        board_id=board_id,
        user_created_id=user.id,
        kind=kind,
        properties=cmd["element"]["properties"],
    )

    try:
        db.add(new_element)
        db.commit()
        db.refresh(new_element)
    except SQLAlchemyError:
        db.rollback()
        return {"type": "error", "detail": "db error creating element"}

    return {
        "type": "element_added",
        "element": {
            "id": str(new_element.id),
            "type": new_element.kind.value,
            "properties": new_element.properties,
        },
        "user_id": str(user.id),
    }


# {
#   "type": "element_updated",
#   "element_id": "uuid",
#   "properties": {
#     "x": 150,
#     "y": 200
#   }
# }
async def cmd_update_element(
    _: UUID, cmd: ElementUpdated, ws: WebSocket, user: User, db: Session
) -> dict[str, Any]:
    element = db.query(Element).filter_by(id=cmd["element_id"]).first()
    if not element:
        return {"type": "error", "detail": "element not found"}

    element.properties = cmd["properties"]

    try:
        db.commit()
        db.refresh(element)
    except SQLAlchemyError:
        db.rollback()
        return {"type": "error", "detail": "db error editing element"}

    return {
        "type": "element_updated",
        "element": {
            "id": str(element.id),
            "type": element.kind.value,
            "properties": element.properties,
        },
        "user_id": str(user.id),
    }


# {
#   "type": "element_deleted",
#   "element_id": "uuid"
# }
async def cmd_element_deleted(
    board_id: UUID, cmd: ElementDeleted, ws: WebSocket, user: User, db: Session
) -> dict[str, Any]:
    element = db.query(Element).filter_by(id=cmd["element_id"]).first()
    if not element:
        return {"type": "error", "detail": "element not found"}

    try:
        db.delete(element)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return {"type": "error", "detail": "db error deleting element"}

    return {
        "type": "element_deleted",
        "element_id": str(cmd["element_id"]),
        "user_id": str(user.id),
    }


# {
#   "type": "cursor_moved",
#   "x": 250,
#   "y": 300
# }
async def cmd_cursor_moved(
    board_id: UUID, cmd: CursorMoved, ws: WebSocket, user: User, db: Session
) -> dict[str, Any]:
    return {"type": "cursor_moved", "x": cmd["x"], "y": cmd["y"]}


HANDLERS: dict[str, Any] = {
    "element_added": cmd_add_element,
    "element_updated": cmd_update_element,
    "element_deleted": cmd_element_deleted,
    "cursor_moved": cmd_cursor_moved,
}


@router.websocket("/{board_id}/ws")
async def ws(
    board_id: UUID,
    websocket: WebSocket,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_ws),
):
    await websocket.accept()

    rooms.setdefault(board_id, set()).add(websocket)
    await broadcast(
        board_id,
        {
            "type": "user_joined",
            "user": {"id": str(user.id), "name": f"{user.first_name} {user.last_name}"},
        },
        exclude=websocket,
    )

    try:
        while True:
            msg = await websocket.receive_json()
            event_type = msg.get("type")

            handler = HANDLERS.get(event_type)
            if not handler:
                await websocket.send_json(
                    {"type": "error", "detail": "unknown event type"}
                )
                continue

            out = await handler(board_id, msg, websocket, user, db)
            await broadcast(board_id, out, exclude=websocket)

    except WebSocketDisconnect:
        rooms.get(board_id, set()).discard(websocket)

        if board_id in rooms and not rooms[board_id]:
            rooms.pop(board_id, None)

        await broadcast(board_id, {"type": "user_left", "user_id": str(user.id)})
