<template>
  <gym-search-card
    :gym-list="fetchGymList"
    :select-item="selectGym"
    :item-title="itemTitle"
  />
</template>

<script>
import GymSearchCard from "~/components/navigation/GymSearchCard.vue"
import actions from "~/store/actions.js"

export default {
  components: {
    GymSearchCard,
  },
  data() {
    return {
      itemTitle: "city",
    }
  },
  computed: {
    fetchGymList: function () {
      if (this.$store.state.gyms !== {}) return this.$store.state.gyms
      return []
    },
    fetchGymsURL: function () {
      const country = this.$store.state["current_country"]
      const state = this.$store.state["current_state"]
      const city = this.$store.state[`current_${this.itemTitle}`]
      let url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`
      if (state != this.$store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`
      url = encodeURI(url)
      return url
    },
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchGyms()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchGyms() {
      const url = this.fetchGymsURL
      actions.retrieveGyms(url, this.$store)
    },
    selectGym(selectedGym) {
      this.$store.commit("SET_GYM_OBJECT", selectedGym)
      this.$pushCleanedRoute(this.$router, `${selectedGym.name}/`)
    },
  },
}
</script>
