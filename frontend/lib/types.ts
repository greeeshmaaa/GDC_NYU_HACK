export type ResolvedPlace = {
  landmark?: string;
  neighborhood?: string;
  borough?: string;
  confidence?: number;
  status: "resolved" | "needs_clarification";
};

export type CaptureResponse =
  | {
      status: "resolved";
      place: ResolvedPlace;
      summary: string;
      available_modes: string[];
    }
  | {
      status: "needs_clarification";
      clarification: {
        message: string;
        options: string[];
      };
    };

export type AskResponse = {
  answer_text: string;
  answer_audio_script: string;
  followups: string[];
};

export type StoryResponse = {
  title: string;
  story_beats: string[];
  highlighted_fact: string;
  why_it_still_matters: string;
  audio_script: string;
};

export type CommunityResponse = {
  community_summary: string;
  nearby_resources: string[];
  environmental_context: string[];
  helpful_actions: string[];
};