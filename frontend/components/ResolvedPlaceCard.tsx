type Props = {
  landmark?: string;
  neighborhood?: string;
  borough?: string;
  summary: string;
};

export default function ResolvedPlaceCard({
  landmark,
  neighborhood,
  borough,
  summary,
}: Props) {
  return (
    <div className="rounded-2xl border border-gray-200 p-4">
      <h2 className="text-xl font-semibold">{landmark}</h2>
      <p className="text-sm text-gray-600">
        {[neighborhood, borough].filter(Boolean).join(", ")}
      </p>
      <p className="mt-3 text-sm">{summary}</p>
    </div>
  );
}