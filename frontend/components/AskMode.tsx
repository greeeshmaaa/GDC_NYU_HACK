type Props = {
  result: {
    answer_text?: string;
    followups?: string[];
  };
};

export default function AskMode({ result }: Props) {
  const followups = result.followups ?? [];

  return (
    <div className="rounded-2xl border border-gray-200 p-4 space-y-3">
      <h3 className="font-semibold">Ask Mode</h3>
      <p>{result.answer_text || "No answer available yet."}</p>

      <div>
        <p className="text-sm font-medium text-gray-700">Follow-ups</p>
        <ul className="mt-2 list-disc pl-5 text-sm text-gray-600">
          {followups.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}