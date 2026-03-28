type Mode = "ask" | "story" | "community";

type Props = {
  activeMode: Mode | null;
  onSelect: (mode: Mode) => void;
};

export default function ModeTabs({ activeMode, onSelect }: Props) {
  const base = "rounded-xl border px-4 py-2 text-sm transition";
  const active = "border-black bg-black text-white";
  const inactive = "border-gray-300 hover:bg-gray-50";

  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onSelect("ask")}
        className={`${base} ${activeMode === "ask" ? active : inactive}`}
      >
        Ask
      </button>
      <button
        onClick={() => onSelect("story")}
        className={`${base} ${activeMode === "story" ? active : inactive}`}
      >
        Story
      </button>
      <button
        onClick={() => onSelect("community")}
        className={`${base} ${activeMode === "community" ? active : inactive}`}
      >
        Community
      </button>
    </div>
  );
}