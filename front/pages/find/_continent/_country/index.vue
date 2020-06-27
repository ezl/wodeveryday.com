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

    if (countryHasStates) {
      const country = route.params["country"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`

      await apiLibrary.retrieveStates(url, store)
    } else {
      const country = route.params["country"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/gyms/?country=${country}`

      await apiLibrary.retrieveCities(url, store)
    }

    return {
      countryHasStates: countryHasStates,
    }
  },
  data() {
    return {
      countryHasStates: false,
    }
  },
}
</script>
