"use client";

import { useState } from "react";
import CameraCapture from "../components/CameraCapture";
import ResolvedPlaceCard from "../components/ResolvedPlaceCard";
import ModeTabs from "../components/ModeTabs";
import AskMode from "../components/AskMode";
import StoryMode from "../components/StoryMode";
import CommunityMode from "../components/CommunityMode";
import {
  captureLandmark,
  clarifyPlace,
  askMode,
  storyMode,
  communityMode,
} from "../lib/api";

type Place = {
  landmark?: string;
  neighborhood?: string;
  borough?: string;
  confidence?: number;
  status?: string;
};

type Mode = "ask" | "story" | "community";

export default function HomePage() {
  const [place, setPlace] = useState<Place | null>(null);
  const [summary, setSummary] = useState("");
  const [clarification, setClarification] = useState<{
    message: string;
    options: string[];
  } | null>(null);
  const [activeMode, setActiveMode] = useState<Mode | null>(null);
  const [modeResult, setModeResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleCapture = async (payload: {
    image_base64: string;
    lat?: number;
    lng?: number;
  }) => {
    try {
      setLoading(true);
      setModeResult(null);
      setActiveMode(null);

      const result = await captureLandmark(payload);

      if (result.status === "needs_clarification") {
        setClarification(result.clarification);
        setPlace(null);
        setSummary("");
        return;
      }

      setClarification(null);
      setPlace(result.place);
      setSummary(result.summary);
    } catch (error) {
      console.error(error);
      alert("Failed to detect landmark.");
    } finally {
      setLoading(false);
    }
  };

  const handleClarify = async (selectedPlace: string) => {
    try {
      setLoading(true);
      setModeResult(null);
      setActiveMode(null);

      const result = await clarifyPlace({ selected_place: selectedPlace });

      setClarification(null);
      setPlace(result.place);
      setSummary(
        `You’re looking at ${selectedPlace}. You can now explore Ask, Story, and Community modes.`
      );
    } catch (error) {
      console.error(error);
      alert("Failed to clarify landmark.");
    } finally {
      setLoading(false);
    }
  };

  const loadMode = async (mode: Mode) => {
    if (!place?.landmark) return;

    try {
      setLoading(true);
      setModeResult(null); // clear previous mode result first
      setActiveMode(mode);

      let result;
      if (mode === "ask") {
        result = await askMode({
          landmark: place.landmark,
          neighborhood: place.neighborhood,
          borough: place.borough,
          question: "Why is this place important?",
        });
      } else if (mode === "story") {
        result = await storyMode({
          landmark: place.landmark,
          neighborhood: place.neighborhood,
          borough: place.borough,
        });
      } else {
        result = await communityMode({
          landmark: place.landmark,
          neighborhood: place.neighborhood,
          borough: place.borough,
        });
      }

      setModeResult(result);
    } catch (error) {
      console.error(error);
      alert(`Failed to load ${mode} mode.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-white px-4 py-8 text-black">
      <div className="mx-auto max-w-3xl space-y-6">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">NYC Lens</h1>
          <p className="text-gray-600">
            Capture a landmark, then explore it through Ask, Story, and Community modes.
          </p>
        </div>

        {!place && !clarification && <CameraCapture onCapture={handleCapture} />}

        {loading && (
          <div className="rounded-2xl border border-gray-200 p-4 text-sm text-gray-600">
            Loading...
          </div>
        )}

        {clarification && (
          <div className="rounded-2xl border border-gray-200 p-4 space-y-4">
            <p className="font-medium">{clarification.message}</p>
            <div className="flex flex-wrap gap-2">
              {clarification.options.map((option) => (
                <button
                  key={option}
                  onClick={() => handleClarify(option)}
                  className="rounded-xl border border-gray-300 px-4 py-2 text-sm hover:bg-gray-50"
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        )}

        {place && (
          <div className="space-y-4">
            <ResolvedPlaceCard
              landmark={place.landmark}
              neighborhood={place.neighborhood}
              borough={place.borough}
              summary={summary}
            />

            <ModeTabs activeMode={activeMode} onSelect={loadMode} />

            {modeResult && activeMode === "ask" && <AskMode result={modeResult} />}
            {modeResult && activeMode === "story" && <StoryMode result={modeResult} />}
            {modeResult && activeMode === "community" && (
              <CommunityMode result={modeResult} />
            )}
          </div>
        )}
      </div>
    </main>
  );
}