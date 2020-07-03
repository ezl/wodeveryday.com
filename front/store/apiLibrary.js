import apiService from "./apiService"

/* eslint-disable no-unused-vars */
export default {
  async retrieveContinents(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data
    if (store) store.commit("SET_CONTINENTS", data)
    return data
  },

  async retrieveCountries(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data
    if (store) store.commit("SET_COUNTRIES", data)
    return data
  },

  async retrieveStates(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data
    if (store) store.commit("SET_STATES", data)
    return data
  },

  async retrieveCities(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data
    if (store) store.commit("SET_CITIES", data)
    return data
  },

  async retrieveGym(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data.results[0]
    if (store) store.commit("SET_GYM_OBJECT", data)
    return data
  },

  async retrieveGyms(url, store = null) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data.results
    if (store) store.commit("SET_GYMS", data)
    return data
  },

  async retrieveGymSlugs(url) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    const data = response.data
    return data
  },

  async retrieveLeaderboardData(url, params) {
    url = encodeURI(url)
    const response = await apiService.get(url, params)
    const data = response.data[0]
    return data
  },

  async retrieveGymDetails(url, store) {
    url = encodeURI(url)
    const response = await apiService.get(url)
    if (response) {
      const data = response.data[0]
      if (store) store.commit("SET_PLACE_DETAILS", data)
      return data
    }
  },

  async retrieveGymPhotos(store, service, request) {
    return new Promise((resolve, reject) => {
      service.getDetails(request, (place, status) => {
        // eslint-disable-next-line no-undef
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          store.commit("SET_PLACE_PHOTOS", place)
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

  async initMap(latitude, longitude) {
    // eslint-disable-next-line no-undef
    var location = new google.maps.LatLng(latitude, longitude)

    // eslint-disable-next-line no-undef
    let map = new google.maps.Map(document.getElementById("map"), {
      center: location,
      zoom: 15,
    })

    // eslint-disable-next-line no-undef
    new google.maps.Marker({
      map: map,
      position: location,
    })

    return map
  },
}
