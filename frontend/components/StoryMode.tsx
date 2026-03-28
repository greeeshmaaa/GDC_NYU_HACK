type Props = {
  result: {
    title?: string;
    story_beats?: string[];
    highlighted_fact?: string;
    why_it_still_matters?: string;
  };
};

export default function StoryMode({ result }: Props) {
  const storyBeats = result.story_beats ?? [];

  return (
    <div className="rounded-2xl border border-gray-200 p-4 space-y-3">
      <h3 className="font-semibold">{result.title || "Story Mode"}</h3>

      <ul className="list-disc pl-5 text-sm text-gray-700 space-y-1">
        {storyBeats.map((beat, idx) => (
          <li key={idx}>{beat}</li>
        ))}
      </ul>

      {result.highlighted_fact && (
        <p className="text-sm">
          <span className="font-medium">Highlighted fact:</span>{" "}
          {result.highlighted_fact}
        </p>
      )}

      {result.why_it_still_matters && (
        <p className="text-sm">
          <span className="font-medium">Why it still matters:</span>{" "}
          {result.why_it_still_matters}
        </p>
      )}
    </div>
  );
}