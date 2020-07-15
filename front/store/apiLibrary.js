import apiService from "./apiService"

/* eslint-disable no-unused-vars */
export default {
  async retrieveContinents(url, store = null) {
    const data = await apiService.get(url)
    if (store) store.commit("SET_CONTINENTS", data)
    return data
  },

  async retrieveCountries(url, store = null) {
    const data = await apiService.get(url)
    if (store) store.commit("SET_COUNTRIES", data)
    return data
  },

  async retrieveStates(url, store = null) {
    const data = await apiService.get(url)
    if (store) store.commit("SET_STATES", data)
    return data
  },

  async retrieveCities(url, store = null) {
    const data = await apiService.get(url)
    if (store) store.commit("SET_CITIES", data)
    return data
  },

  async retrieveGym(url, store = null) {
    let data = await apiService.get(url)
    data = data.results[0]
    if (store) store.commit("SET_GYM_OBJECT", data)
    return data
  },

  async retrieveGyms(url, store = null) {
    let data = await apiService.get(url)
    data = data.results
    if (store) store.commit("SET_GYMS", data)
    return data
  },

  async searchLocations(url) {
    const data = await apiService.get(url)
    return data
  },

  async retrieveGymSlugs(url) {
    const data = await apiService.get(url)
    return data
  },

  async retrieveLeaderboardData(url, params) {
    try {
      let data = await apiService.get(url, params)
      data = data[0]
      return data
    } catch (e) {
      return {}
    }
  },

  async retrieveGymDetails(url, store) {
    try {
      let data = await apiService.get(url)
      data = data[0]
      if (store) store.commit("SET_PLACE_DETAILS", data)
      return data
    } catch (e) {
      if (store) store.commit("SET_PLACE_DETAILS", {})
      return {}
    }
  },

  async updateGymDetails(url, payload) {
    try {
      const data = await apiService.put(url, payload)
      return data
    } catch (e) {
      return {}
    }
  },

  async retrieveGymPhotos(store, service, request) {
    return new Promise((resolve, reject) => {
      service.getDetails(request, (place, status) => {
        // eslint-disable-next-line no-undef
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          if (place.photos) this.storePlacePhotoData(store, place)
          resolve(place)
        }
        reject(status)
      })
    })
  },

  storePlacePhotoData(store, place) {
    let placePhotos = place.photos
    placePhotos = this.extractPlacePhotoData(placePhotos)
    store.commit("UPDATE_PLACE_DETAILS_PHOTOS", placePhotos)
    placePhotos = { photos: placePhotos }
    store.commit("SET_PLACE_PHOTOS", placePhotos)
  },

  extractPlacePhotoData(placePhotos) {
    placePhotos.map((photoObj, index) => {
      placePhotos[index].photo_url = photoObj.getUrl()
    })
    return placePhotos
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
