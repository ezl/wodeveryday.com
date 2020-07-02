<template>
  <div>
    <city-and-gym-select v-if="countryHasStates" />
    <gym-select v-if="!countryHasStates" />
  </div>
</template>

<script>
import CityAndGymSelect from "~/components/navigation/CityAndGymSelect.vue"
import GymSelect from "~/components/navigation/GymSelect.vue"
import apiLibrary from "~/store/apiLibrary.js"
import _ from "lodash"
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

export default {
  components: {
    CityAndGymSelect,
    GymSelect,
  },
  async asyncData({ route, store }) {
    let countryHasStates = route.fullPath
      .split("/")
      .filter(Boolean)
      .some((r) => ["united-states", "australia", "canada"].indexOf(r) >= 0)
    let pageDescription = ""
    if (countryHasStates) {
      const state = route.params["state"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/gyms/?state=${state}`
      await apiLibrary.retrieveCities(url, store)

      // generate page description
      const gymLists = Object.values(store.state.cities)
      let numberOfGyms = 0
      gymLists.forEach((list) => {
        numberOfGyms += list.length
      })
      const numberOfCities = Object.keys(store.state.cities).length
      let locationName = "state"
      if (numberOfGyms.length > 0) locationName = "states"
      pageDescription = `${numberOfGyms} gym${
        numberOfGyms.length > 0 ? "s" : ""
      } across ${numberOfCities} ${locationName}. Find the best CrossFit Gym in your City. Photos, Pricing, Contact Information and All You Need To Know Before Visiting`
    } else {
      const country = route.params["country"].replace(/-/gi, " ")
      const city = route.params["state"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`
      await apiLibrary.retrieveGyms(url, store)
      const cityName = _.capitalize(city)
      pageDescription = `The ${store.state.gyms.length} Best CrossFit Gym${
        store.state.gyms.length > 1 ? "s" : ""
      } in ${cityName}. Check Out The Latest Reviews, Pricing, Contact Information for CrossFit Gyms in ${cityName}`
    }

    let pageTitle = store.state.constants.GEO_PAGE_TITLE.replace(
      "{}",
      _.capitalize(route.params["state"]).replace(/-/gi, " ")
    )

    let metaTags = reusableFunctionsLibrary.generateMetaTags(
      store,
      pageTitle,
      pageDescription,
      store.state.constants.DEFAULT_GYM_THUMBNAIL,
      route.fullPath
    )

    return {
      countryHasStates: countryHasStates,
      metaTags: metaTags,
      pageTitle: pageTitle,
    }
  },
  data() {
    return {
      countryHasStates: false,
      metaTags: [],
    }
  },
  head() {
    return {
      title: this.pageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
