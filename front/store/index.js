import Vue from "vue"

// =================================================
// State
// =================================================
export const state = () => {
  const s = {
    gym_navbar_options: [],
    gym_navbar_goto_elements: [],
    global_bread_crumb_names: [],
    global_bread_crumb_paths: [],
    gym_object: {},
    gyms: [],
    continents: {},
    countries: {},
    states: {},
    cities: {},
    place_details: {},
    place_photos: {},
  }

  return s
}
export const initialState = state

// =================================================
// Mutations
// =================================================
export const mutations = {
  UPDATE_PLACE_DETAILS_PHOTOS: (state, photos) => {
    let place_details = state.place_details
    place_details["photos"] = photos
    Vue.set(state, "place_details", place_details)
  },
  SET_PLACE_DETAILS: (state, place_details) => {
    Vue.set(state, "place_details", place_details)
  },
  SET_PLACE_PHOTOS: (state, place_photos) => {
    Vue.set(state, "place_photos", place_photos)
  },
  RESET_STATE: (state) => {
    const s = initialState()
    Object.keys(s).forEach((key) => {
      state[key] = s[key]
    })
  },
  PUSH_TO_GYM_NAVBAR_OPTIONS: (state, gymNavbarOption) => {
    state["gym_navbar_options"].push(gymNavbarOption)
  },
  UNSHIFT_TO_GYM_NAVBAR_OPTIONS: (state, gymNavbarOption) => {
    if (typeof gymNavbarOption === "object") {
      state["gym_navbar_options"].unshift(...gymNavbarOption)
    } else {
      state["gym_navbar_options"].unshift(gymNavbarOption)
    }
  },
  SET_GYM_NAVBAR_OPTIONS: (state, gym_navbar_options) => {
    Vue.set(state, "gym_navbar_options", gym_navbar_options)
  },
  PUSH_TO_GYM_NAVBAR_GOTO_ELEMENTS: (state, gymNavbarGotoElement) => {
    state["gym_navbar_goto_elements"].push(gymNavbarGotoElement)
  },
  UNSHIFT_TO_GYM_NAVBAR_GOTO_ELEMENTS: (state, gymNavbarGotoElement) => {
    if (typeof gymNavbarGotoElement === "object") {
      state["gym_navbar_goto_elements"].unshift(...gymNavbarGotoElement)
    } else {
      state["gym_navbar_goto_elements"].unshift(gymNavbarGotoElement)
    }
  },
  SET_GYM_NAVBAR_GOTO_ELEMENTS: (state, gym_navbar_goto_elements) => {
    Vue.set(state, "gym_navbar_goto_elements", gym_navbar_goto_elements)
  },
  SET_GLOBAL_BREADCRUMB_NAMES: (state, global_bread_crumb_names) => {
    Vue.set(state, "global_bread_crumb_names", global_bread_crumb_names)
  },
  SET_GLOBAL_BREADCRUMB_PATHS: (state, global_bread_crumb_paths) => {
    Vue.set(state, "global_bread_crumb_paths", global_bread_crumb_paths)
  },
  SET_GYM_OBJECT: (state, gym_object) => {
    Vue.set(state, "gym_object", gym_object)
  },
  SET_GYMS: (state, gyms) => {
    Vue.set(state, "gyms", gyms)
  },
  SET_CONTINENTS: (state, continents) => {
    Vue.set(state, "continents", continents)
  },
  SET_COUNTRIES: (state, countries) => {
    Vue.set(state, "countries", countries)
  },
  SET_STATES: (state, states) => {
    Vue.set(state, "states", states)
  },
  SET_CITIES: (state, cities) => {
    Vue.set(state, "cities", cities)
  },
}
