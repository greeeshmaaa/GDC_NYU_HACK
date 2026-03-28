"use client";

import { useEffect, useRef, useState } from "react";

type Props = {
  onCapture: (payload: {
    image_base64: string;
    lat?: number;
    lng?: number;
  }) => void;
};

export default function CameraCapture({ onCapture }: Props) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  const [coords, setCoords] = useState<{ lat?: number; lng?: number }>({});
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch {
        setError("Unable to access camera.");
      }
    }

    function setupLocation() {
      if (!navigator.geolocation) return;

      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoords({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        () => {
          console.log("Location permission denied or unavailable.");
        }
      );
    }

    setupCamera();
    setupLocation();
  }, []);

  const handleCapture = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    const width = video.videoWidth || 640;
    const height = video.videoHeight || 480;

    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, width, height);
    const image_base64 = canvas.toDataURL("image/jpeg");

    onCapture({
      image_base64,
      lat: coords.lat,
      lng: coords.lng,
    });
  };

  return (
    <div className="space-y-4">
      <div className="overflow-hidden rounded-2xl border border-gray-200">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="h-auto w-full bg-black"
        />
      </div>

      <canvas ref={canvasRef} className="hidden" />

      {error && <p className="text-sm text-red-500">{error}</p>}

      <button
        onClick={handleCapture}
        className="w-full rounded-2xl bg-black px-4 py-3 text-white transition hover:opacity-90"
      >
        Capture Landmark
      </button>
    </div>
  );
}