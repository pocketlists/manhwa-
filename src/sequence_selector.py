import os, json, base64
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class SequenceSelector:
    def __init__(self, images_dir, transcript_lines):
        self.images_dir = images_dir
        self.transcript_lines = transcript_lines
        self.image_files = sorted([f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])

    # METHOD 1: OpenAI Text Matching (Fastest & Cheapest)
    def method_text_matching(self, api_key):
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""
        Given this story transcript: {self.transcript_lines}
        And these image filenames: {self.image_files}
        Sort the filenames in the exact story order. Return ONLY a JSON array of filenames.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    # METHOD 2: OpenAI Vision AI (Most Accurate)
    def method_vision_ai(self, api_key):
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        base64_images = []
        for img in self.image_files:
            with open(os.path.join(self.images_dir, img), "rb") as f:
                base64_images.append(base64.b64encode(f.read()).decode('utf-8'))
        prompt = f"Here are the transcript lines: {self.transcript_lines}. Match these images to the story order. Return JSON array of filenames."
        content = [{"type": "text", "text": prompt}]
        for b64 in base64_images:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}]
        )
        return json.loads(response.choices[0].message.content)

    # METHOD 3: Local CLIP (100% Free & Private)
    def method_local_clip(self):
        model = SentenceTransformer('clip-ViT-B-32')
        image_embeddings = model.encode([os.path.join(self.images_dir, f) for f in self.image_files])
        text_embeddings = model.encode(self.transcript_lines)
        sim_matrix = cosine_similarity(image_embeddings, text_embeddings)
        assigned_order = []
        used_images = set()
        for line_idx in range(len(self.transcript_lines)):
            best_img_idx = -1
            best_score = -1
            for img_idx in range(len(self.image_files)):
                if img_idx not in used_images and sim_matrix[img_idx][line_idx] > best_score:
                    best_score = sim_matrix[img_idx][line_idx]
                    best_img_idx = img_idx
            used_images.add(best_img_idx)
            assigned_order.append(self.image_files[best_img_idx])
        return assigned_order
