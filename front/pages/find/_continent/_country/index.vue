<template>
  <div>
    <state-and-city-select v-if="countryHasStates" />
    <city-and-gym-select v-if="!countryHasStates" />
  </div>
</template>

<script>
import CityAndGymSelect from "~/components/navigation/CityAndGymSelect.vue"
import StateAndCitySelect from "~/components/navigation/StateAndCitySelect.vue"
import apiLibrary from "~/store/apiLibrary.js"
import _ from "lodash"
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

export default {
  components: {
    CityAndGymSelect,
    StateAndCitySelect,
  },
  async asyncData({ route, store }) {
    let countryHasStates = route.fullPath
      .split("/")
      .filter(Boolean)
      .some((r) => ["united-states", "australia", "canada"].indexOf(r) >= 0)

    let pageDescription = store.state.constants.DEFAULT_GYM_THUMBNAIL

    if (countryHasStates) {
      const country = route.params["country"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`
      await apiLibrary.retrieveStates(url, store)
    } else {
      // fetch cities and their gyms
      const country = route.params["country"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/gyms/?country=${country}`
      await apiLibrary.retrieveCities(url, store)

      // generate page description
      const gymLists = Object.values(store.state.cities)
      let numberOfGyms = 0
      gymLists.forEach((list) => {
        numberOfGyms += list.length
      })
      const numberOfCities = Object.keys(store.state.cities).length
      let locationName = "city"
      if (numberOfGyms.length > 1) locationName = "cities"
      pageDescription = `${numberOfGyms} gym${
        numberOfGyms.length > 1 ? "s" : ""
      } across ${numberOfCities} ${locationName}. Find the best CrossFit Gym in your City. Photos, Pricing, Contact Information and All You Need To Know Before Visiting`
    }

    let pageTitle = store.state.constants.GEO_PAGE_TITLE.replace(
      "{}",
      _.capitalize(route.params["country"]).replace(/-/gi, " ")
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
      pageTitle: "",
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
