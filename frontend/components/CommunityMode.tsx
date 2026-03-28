type Props = {
  result: {
    community_summary?: string;
    nearby_resources?: string[];
    environmental_context?: string[];
    helpful_actions?: string[];
  };
};

export default function CommunityMode({ result }: Props) {
  const nearbyResources = result.nearby_resources ?? [];
  const environmentalContext = result.environmental_context ?? [];
  const helpfulActions = result.helpful_actions ?? [];

  return (
    <div className="rounded-2xl border border-gray-200 p-4 space-y-4">
      <h3 className="font-semibold">Community Mode</h3>
      <p>{result.community_summary || "No community summary available yet."}</p>

      <div>
        <p className="text-sm font-medium text-gray-700">Nearby resources</p>
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-600">
          {nearbyResources.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>

      <div>
        <p className="text-sm font-medium text-gray-700">Environmental context</p>
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-600">
          {environmentalContext.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>

      <div>
        <p className="text-sm font-medium text-gray-700">Helpful actions</p>
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-600">
          {helpfulActions.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}