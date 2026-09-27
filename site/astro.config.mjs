// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Vercel sets VERCEL_URL automatically; for local dev, omit `site`
  // to avoid mismatches. Set it explicitly only if you have a custom domain.
  ...(process.env.VERCEL_URL && { site: `https://${process.env.VERCEL_URL}` }),
  output: 'static',
  build: {
    assets: '_assets',
  },
  vite: {
    build: {
      cssMinify: true,
    },
  },
});
