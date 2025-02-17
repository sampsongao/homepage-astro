
import { type Dispatch, type SetStateAction, useEffect, useState } from "react";

export default function useDarkMode() {
  const [darkModeOn, setDarkModeOn] = useState(true);

  useEffect(() => {
    setDarkModeOn(localStorage?.getItem("darkModeOn") !== undefined
      ? localStorage?.getItem("darkModeOn") === 'true'
      : window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    );

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const updateDarkMode = (e: MediaQueryListEvent) => {
      setDarkModeOn(e.matches);
    };

    // Register listener
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateDarkMode);

    // Clean up listener
    return () => window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', updateDarkMode);
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    if (darkModeOn) {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }

    localStorage?.setItem("darkModeOn", JSON.stringify(darkModeOn));
  }, [darkModeOn]);

  return [darkModeOn, setDarkModeOn] as [boolean, Dispatch<SetStateAction<boolean>>];
}
