import { createContext, useContext, useState } from 'react';

const SavedContext = createContext();

export function SavedProvider({ children }) {
  const [saved, setSaved] = useState([]);

  function toggleSaved(station) {
    setSaved(prev =>
      prev.find(s => s.id === station.id)
        ? prev.filter(s => s.id !== station.id)
        : [...prev, station]
    );
  }

  function isSaved(id) {
    return saved.some(s => s.id === id);
  }

  return (
    <SavedContext.Provider value={{ saved, toggleSaved, isSaved }}>
      {children}
    </SavedContext.Provider>
  );
}

export function useSaved() {
  return useContext(SavedContext);
}