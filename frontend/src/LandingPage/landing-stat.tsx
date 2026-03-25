interface LandingStatProps {
  value: string;
  label: string;
}

export const LandingStat = ({ value, label }: LandingStatProps) => {
  return (
    <div className="rounded-3xl border border-white/10 bg-black/70 px-5 py-4 shadow-sm backdrop-blur">
      <p className="text-2xl font-semibold text-slate-50">{value}</p>
      <p className="mt-1 text-sm text-slate-400">{label}</p>
    </div>
  );
};
