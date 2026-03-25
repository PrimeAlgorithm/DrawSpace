interface ApiFetchOptions extends RequestInit {
    redirectOnUnauthorized?: boolean;
}

export async function apiFetch(url: string, options?: ApiFetchOptions): Promise<Response> {
    const { redirectOnUnauthorized = true, ...fetchOptions } = options ?? {};
    const res = await fetch(url, {
        credentials: "include",
        ...fetchOptions,
    });
    if (redirectOnUnauthorized && res.status === 401) {
        window.location.href = "/login";
    }
    return res;
}
