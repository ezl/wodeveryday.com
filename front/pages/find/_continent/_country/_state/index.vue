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

    if (countryHasStates) {
      const state = route.params["state"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/gyms/?state=${state}`

      await apiLibrary.retrieveCities(url, store)
    } else {
      const country = route.params["country"].replace(/-/gi, " ")
      const city = route.params["state"].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`

      await apiLibrary.retrieveGyms(url, store)
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
