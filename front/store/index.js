import Vue from "vue"

// =================================================
// State
// =================================================
export const state = () => {
  const s = {
    current_affiliate: {},
  }

  return s
}

// =================================================
// Mutations
// =================================================
export const mutations = {
  SET_CURRENT_AFFILIATE: (state, affiliate) => {
    if (affiliate) {
      Vue.set(state, "current_affiliate", affiliate)
    }
  },
}
