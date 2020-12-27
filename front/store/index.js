export const actions = {
  async searchLocation({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/search_locations/', {
        params: payload
      }).then(response => {
        resolve(response.data.data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  async getContinents({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/continents/', {
        params: payload
      }).then(response => {
        resolve(
          response.data
        )
      }).catch(error => {
        reject(error)
      })
    })
  },
  async getCountries({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/countries/', {
        params: payload
      }).then(response => {
        resolve(
          response.data
        )
      }).catch(error => {
        reject(error)
      })
    })
  },
  async getStates({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/states/', {
        params: payload
      }).then(response => {
        resolve(
          response.data
        )
      }).catch(error => {
        reject(error)
      })
    })
  },
  async getGyms({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/gyms/', {
        params: payload
      }).then(response => {
        resolve(
          response.data
        )
      }).catch(error => {
        reject(error)
      })
    })
  },
  async getGymsByCity({}, payload) {
    return new Promise((resolve, reject) => {
      this.$axios.get('gyms/', {
        params: payload
      }).then(response => {
        resolve(
          response.data
        )
      }).catch(error => {
        reject(error)
      })
    })
  },

}
export const state = () => ({
  COUNTRIES_WITH_STATES: ["united-states", "australia", "canada"],
})
export const getters = {
  countries_with_countries: state => {
    return state.COUNTRIES_WITH_STATES
  }
}
export const mutations = {}
