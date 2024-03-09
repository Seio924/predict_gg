import { atom } from "recoil";

export const showMainPageState = atom({
  key: "showMainPageState",
  default: true,
});

export const setResultPageActiveState = atom({
  key: "setResultPageActiveState",
  default: false,
});

export const championNameState = atom<string[]>({
  key: "championNameState",
  default: [],
});

export const summonerNameState = atom<string[]>({
  key: "summonerNameState",
  default: [],
});

export const teamIdState = atom<number[]>({
  key: "teamIdState",
  default: [],
});

export const assistsState = atom<number[]>({
  key: "assistsState",
  default: [],
});

export const deathsState = atom<number[]>({
  key: "deathsState",
  default: [],
});

export const killsState = atom<number[]>({
  key: "killsState",
  default: [],
});

export const winningRateState = atom<number[][]>({
  key: "winningRateState",
  default: [],
});
