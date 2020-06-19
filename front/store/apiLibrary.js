import apiService from "./apiService"

/* eslint-disable no-unused-vars */
export default {
  async retrieveContinents(url, store) {
    const response = await apiService.get(url)
    const data = response.data
    store.commit("SET_CONTINENTS", data)
    return data
  },

  async retrieveCountries(url, store) {
    const response = await apiService.get(url)
    const data = response.data
    store.commit("SET_COUNTRIES", data)
    return data
  },

  async retrieveStates(url, store) {
    const response = await apiService.get(url)
    const data = response.data
    store.commit("SET_STATES", data)
    return data
  },

  async retrieveCities(url, store) {
    const response = await apiService.get(url)
    const data = response.data
    store.commit("SET_CITIES", data)
    return data
  },

  async retrieveGym(url, store) {
    const response = await apiService.get(url)
    const data = response.data.results[0]
    store.commit("SET_GYM_OBJECT", data)
    return data
  },

  async retrieveGyms(url, store) {
    const response = await apiService.get(url)
    const data = response.data.results
    store.commit("SET_GYMS", data)
    return data
  },

  async retrieveLeaderboardData(url, params) {
    const response = await apiService.get(url, params)
    const data = response.data
    return data
  },

  async retrieveGymDetails(service, request) {
    return new Promise((resolve, reject) => {
      service.getDetails(request, (place, status) => {
        // eslint-disable-next-line no-undef
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          resolve(place)
        }
        reject(status)
      })
    })
  },

  async retrieveGymId(service, request) {
    // eslint-disable-next-line no-unused-vars
    return new Promise((resolve, reject) => {
      service.findPlaceFromQuery(request, (results, status) => {
        if (results != null) {
          resolve(results[0].place_id)
        }
        reject(status)
      })
    })
  },
}
