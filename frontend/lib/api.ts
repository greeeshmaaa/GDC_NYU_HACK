const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export async function captureLandmark(payload: {
  image_base64: string;
  lat?: number;
  lng?: number;
  heading?: number;
}) {
  const res = await fetch(`${API_BASE}/capture`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to capture landmark");
  }

  return res.json();
}

export async function clarifyPlace(payload: {
  selected_place: string;
  lat?: number;
  lng?: number;
}) {
  const res = await fetch(`${API_BASE}/clarify`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to clarify place");
  }

  return res.json();
}

export async function askMode(payload: {
  landmark: string;
  neighborhood?: string;
  borough?: string;
  question: string;
}) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to load ask mode");
  }

  return res.json();
}

export async function storyMode(payload: {
  landmark: string;
  neighborhood?: string;
  borough?: string;
}) {
  const res = await fetch(`${API_BASE}/story`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to load story mode");
  }

  return res.json();
}

export async function communityMode(payload: {
  landmark: string;
  neighborhood?: string;
  borough?: string;
  lat?: number;
  lng?: number;
}) {
  const res = await fetch(`${API_BASE}/community`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to load community mode");
  }

  return res.json();
}