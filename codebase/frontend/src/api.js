async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.detail || "Có lỗi khi gọi API.");
  }

  return data;
}

export const api = {
  health: () => request("/api/health"),
  stylebook: () => request("/api/stylebook"),
  sample: () => request("/api/sample"),
  generate: (sentences, stylebook) =>
    request("/api/storyboard", {
      method: "POST",
      body: JSON.stringify({ sentences, stylebook })
    }),
  revise: (scene, feedback, stylebook, originalSentence) =>
    request(`/api/scenes/${scene.n}/revise`, {
      method: "POST",
      body: JSON.stringify({
        scene,
        feedback,
        stylebook,
        original_sentence: originalSentence || null
      })
    })
};
