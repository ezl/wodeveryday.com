import Vue from "vue"

// =================================================
// State
// =================================================
export const state = () => {
  const s = {
    gymNavbarOptions: [],
    gymNavbarGotoElements: [],
    globalBreadcrumbNames: [],
    globalBreadcrumbPaths: [],
    gym_object: {},
    gyms: [],
    current_gym: undefined,
    continents: {},
    current_continent: undefined,
    countries: {},
    current_country: undefined,
    states: {},
    current_state: undefined,
    cities: {},
    current_city: undefined,
  }

  return s
}
export const initialState = state

// =================================================
// Mutations
// =================================================
export const mutations = {
  RESET_STATE: (state) => {
    const s = initialState()
    Object.keys(s).forEach((key) => {
      state[key] = s[key]
    })
  },
  PUSH_TO_GYM_NAVBAR_OPTIONS: (state, gymNavbarOption) => {
    state["gymNavbarOptions"].push(gymNavbarOption)
  },
  UNSHIFT_TO_GYM_NAVBAR_OPTIONS: (state, gymNavbarOption) => {
    if (typeof gymNavbarOption === "object") {
      state["gymNavbarOptions"].unshift(...gymNavbarOption)
    } else {
      state["gymNavbarOptions"].unshift(gymNavbarOption)
    }
  },
  SET_GYM_NAVBAR_OPTIONS: (state, gymNavbarOptions) => {
    if (gymNavbarOptions) {
      Vue.set(state, "gymNavbarOptions", gymNavbarOptions)
    }
  },
  PUSH_TO_GYM_NAVBAR_GOTO_ELEMENTS: (state, gymNavbarGotoElement) => {
    state["gymNavbarGotoElements"].push(gymNavbarGotoElement)
  },
  UNSHIFT_TO_GYM_NAVBAR_GOTO_ELEMENTS: (state, gymNavbarGotoElement) => {
    if (typeof gymNavbarGotoElement === "object") {
      state["gymNavbarGotoElements"].unshift(...gymNavbarGotoElement)
    } else {
      state["gymNavbarGotoElements"].unshift(gymNavbarGotoElement)
    }
  },
  SET_GYM_NAVBAR_GOTO_ELEMENTS: (state, gymNavbarGotoElements) => {
    if (gymNavbarGotoElements) {
      Vue.set(state, "gymNavbarGotoElements", gymNavbarGotoElements)
    }
  },
  SET_GLOBAL_BREADCRUMB_NAMES: (state, globalBreadcrumbNames) => {
    if (globalBreadcrumbNames) {
      Vue.set(state, "globalBreadcrumbNames", globalBreadcrumbNames)
    }
  },
  SET_GLOBAL_BREADCRUMB_PATHS: (state, globalBreadcrumbPaths) => {
    if (globalBreadcrumbPaths) {
      Vue.set(state, "globalBreadcrumbPaths", globalBreadcrumbPaths)
    }
  },
  SET_GYM_OBJECT: (state, gym_object) => {
    if (gym_object) {
      Vue.set(state, "gym_object", gym_object)
    }
  },
  SET_GYMS: (state, gyms) => {
    if (gyms) {
      Vue.set(state, "gyms", gyms)
    }
  },
  SET_CURRENT_GYM: (state, current_gym) => {
    if (current_gym) {
      Vue.set(state, "current_gym", current_gym)
    }
  },
  SET_CONTINENTS: (state, continents) => {
    if (continents) {
      Vue.set(state, "continents", continents)
    }
  },
  SET_CURRENT_CONTINENT: (state, current_continent) => {
    if (current_continent) {
      Vue.set(state, "current_continent", current_continent)
    }
  },
  SET_COUNTRIES: (state, countries) => {
    if (countries) {
      Vue.set(state, "countries", countries)
    }
  },
  SET_CURRENT_COUNTRY: (state, current_country) => {
    if (current_country) {
      Vue.set(state, "current_country", current_country)
    }
  },
  SET_STATES: (state, states) => {
    if (states) {
      Vue.set(state, "states", states)
    }
  },
  SET_CURRENT_STATE: (state, current_state) => {
    if (current_state) {
      Vue.set(state, "current_state", current_state)
    }
  },
  SET_CITIES: (state, cities) => {
    if (cities) {
      Vue.set(state, "cities", cities)
    }
  },
  SET_CURRENT_CITY: (state, current_city) => {
    if (current_city) {
      Vue.set(state, "current_city", current_city)
    }
  },
}
