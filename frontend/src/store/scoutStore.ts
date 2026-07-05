import { create } from 'zustand';

interface ScoutFilters {
  q: string;
  category: string;
  city: string;
  smartFilters: string[];
}

interface ScoutState {
  filters: ScoutFilters;
  setFilters: (filters: Partial<ScoutFilters>) => void;
  selectedRows: Record<string, boolean>;
  setSelectedRows: (updaterOrValue: Record<string, boolean> | ((old: Record<string, boolean>) => Record<string, boolean>)) => void;
  selectedLeadId: string | null;
  setSelectedLeadId: (id: string | null) => void;
  isDrawerOpen: boolean;
  setIsDrawerOpen: (isOpen: boolean) => void;
  resetFilters: () => void;
  isDiscovering: boolean;
  setIsDiscovering: (status: boolean) => void;
  discoveryStatus: string;
  setDiscoveryStatus: (status: string) => void;
}

const initialFilters: ScoutFilters = {
  q: '',
  category: '',
  city: '',
  smartFilters: [],
};

export const useScoutStore = create<ScoutState>((set) => ({
  filters: initialFilters,
  setFilters: (newFilters) => set((state) => ({ 
    filters: { ...state.filters, ...newFilters } 
  })),
  selectedRows: {},
  setSelectedRows: (updaterOrValue) => set((state) => {
    const newRows = typeof updaterOrValue === 'function' 
      ? updaterOrValue(state.selectedRows) 
      : updaterOrValue;
    return { selectedRows: newRows };
  }),
  selectedLeadId: null,
  setSelectedLeadId: (id) => set({ selectedLeadId: id }),
  isDrawerOpen: false,
  setIsDrawerOpen: (isOpen) => set({ isDrawerOpen: isOpen }),
  resetFilters: () => set({ filters: initialFilters }),
  isDiscovering: false,
  setIsDiscovering: (status) => set({ isDiscovering: status }),
  discoveryStatus: '',
  setDiscoveryStatus: (status) => set({ discoveryStatus: status }),
}));
