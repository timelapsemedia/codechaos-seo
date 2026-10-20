import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Mask, Grain, Roll} from '../components/primitives';
import {useFonts} from '../components/useFonts';
import {F, easeIn, easeOut, prog, sp, clamp01} from '../lib';
import TL from './timeline.json';
import CFG from './config.json';
import AUDIO from './audio.json';

export const REEL_FPS = TL.fps;
export const REEL_W = 1080;
export const REEL_H = 1920;

// Code Chaos palette by default (dark, copper); config.json can override any token
const P = {
  ...{
  bg: '#0C0A09',
  cell: 'rgba(245,236,228,0.06)',
  line: 'rgba(245,236,228,0.12)',
  cream: '#F5ECE4',
  creamDim: 'rgba(245,236,228,0.66)',
  muted: 'rgba(245,236,228,0.40)',
  copper: '#D67834',
  hot: '#FFAA50',
  },
  ...CFG.palette,
};

const ROWS: {key: 'high' | 'mid' | 'low'; label: string}[] = (['high', 'mid', 'low'] as const).map((key, i) => ({key, label: CFG.rows[i]}));
const COLS = 16;

const level = (key: 'high' | 'mid' | 'low', f: number) => {
  const a = AUDIO[key];
  return f >= 0 && f < a.length ? a[f] : 0;
};

/** Step grid driven by the product's real audio (audio.json from scripts/onsets.py): newest frame on the right, history scrolls left. */
const BlastGrid: React.FC<{frame: number; y: number}> = ({frame, y}) => {
  const x0 = 170;
  const cw = 46;
  const gap = 6;
  const ch = 92;
  return (
    <div style={{position: 'absolute', left: 0, top: y, width: REEL_W}}>
      {ROWS.map((row, r) => (
        <div key={row.key} style={{position: 'absolute', top: r * (ch + 18), left: 0, width: REEL_W}}>
          <div style={{position: 'absolute', left: 40, top: ch / 2 - 14, fontFamily: F.mono, fontSize: 26,
            letterSpacing: '0.2em', color: P.muted}}>{row.label}</div>
          {Array.from({length: COLS}, (_, c) => {
            const v = level(row.key, frame - (COLS - 1 - c));
            const lit = clamp01((v - 0.25) / 0.6);
            const newest = c === COLS - 1;
            return (
              <div key={c} style={{position: 'absolute', left: x0 + c * (cw + gap), top: 0, width: cw, height: ch,
                borderRadius: 6, background: P.cell, border: `1px solid ${P.line}`, overflow: 'hidden'}}>
                <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: `${Math.round(v * 100)}%`,
                  background: newest ? P.hot : P.copper, opacity: 0.25 + 0.75 * lit}} />
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const Stat: React.FC<{n: string; label: string; k: number; out: number}> = ({n, label, k, out}) => (
  <div style={{width: 300, textAlign: 'center', opacity: Math.min(1, k * 3) * (1 - out), transform: `translateY(${-out * 40}px)`}}>
    <div style={{fontFamily: F.serif, fontSize: 150, lineHeight: 1, color: P.cream}}>
      <Roll a="0" b={n} k={k} />
    </div>
    <div style={{fontFamily: F.mono, fontSize: 26, letterSpacing: '0.16em', color: P.muted, marginTop: 14,
      opacity: k}}>{label}</div>
  </div>
);

export const Reel: React.FC = () => {
  useFonts();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const kick = level('low', frame);
  const glow = 0.25 + 0.55 * kick;

  const statsOut = prog(t, TL.s2.exit, TL.s2.exit + 0.45, easeIn);
  const priceK = sp(frame, TL.s3.price, {damping: 9, stiffness: 200, mass: 0.7}, fps);
  const formatsK = prog(t, TL.s3.formats, TL.s3.formats + 0.8, easeOut);
  const ctaK = prog(t, TL.s3.cta, TL.s3.cta + 0.8, easeOut);
  const subK = prog(t, TL.s1.sub, TL.s1.sub + 0.8, easeOut);
  // the title "lands" on the first kick: settles from 1.035 to 1
  const titleScale = 1 + 0.035 * (1 - sp(frame, TL.s1.titleSettle, {damping: 15, stiffness: 140, mass: 0.8}, fps));

  return (
    <AbsoluteFill style={{background: P.bg}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse 70% 40% at 50% 52%, rgba(214,120,52,${0.05 + 0.2 * glow}) 0%, rgba(214,120,52,0) 70%)`}} />

      <div style={{position: 'absolute', top: 250, width: REEL_W, textAlign: 'center', fontFamily: F.mono, fontSize: 26,
        letterSpacing: '0.24em', color: P.copper}}>{CFG.kicker}</div>

      <div style={{position: 'absolute', top: 320, width: REEL_W, textAlign: 'center', transform: `scale(${titleScale})`}}>
        <div style={{fontFamily: F.serif, fontSize: 196, lineHeight: 1, letterSpacing: '-0.02em', color: P.cream}}>{CFG.title1}</div>
        <div style={{fontFamily: F.serif, fontStyle: 'italic', fontSize: 196, lineHeight: 1, letterSpacing: '-0.02em', color: P.copper}}>{CFG.title2}</div>
      </div>

      <div style={{position: 'absolute', top: 760, width: REEL_W, textAlign: 'center', fontFamily: F.sans, fontSize: 40,
        color: P.creamDim}}>
        <Mask k={subK}>{CFG.subtitle}</Mask>
      </div>

      <BlastGrid frame={frame} y={900} />

      {/* stats, then price in the same slot */}
      <div style={{position: 'absolute', top: 1330, left: 90, width: 900, display: 'flex', justifyContent: 'space-between'}}>
        {CFG.stats.map((st: {n: string; label: string}, i: number) => (
          <Stat key={i} n={st.n} label={st.label} k={prog(t, TL.s2.stats[i], TL.s2.stats[i] + 0.7, easeOut)} out={statsOut} />
        ))}
      </div>

      <div style={{position: 'absolute', top: 1290, width: REEL_W, textAlign: 'center'}}>
        <div style={{fontFamily: F.serif, fontSize: 210, lineHeight: 1, color: P.hot,
          opacity: clamp01(priceK * 1.5), transform: `scale(${0.7 + 0.3 * priceK})`}}>{CFG.price}</div>
        <div style={{fontFamily: F.mono, fontSize: 26, letterSpacing: '0.2em', color: P.creamDim, marginTop: 26}}>
          <Mask k={formatsK}>{CFG.formats}</Mask>
        </div>
        <div style={{fontFamily: F.sans, fontWeight: 600, fontSize: 46, color: P.cream, marginTop: 40}}>
          <Mask k={ctaK}>{CFG.cta}</Mask>
        </div>
      </div>

      <Grain frame={frame} opacity={0.08} />
    </AbsoluteFill>
  );
};
