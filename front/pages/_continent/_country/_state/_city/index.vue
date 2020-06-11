<template>
  <gym-search-page
    :gym-list="fetchGymList"
    :select-item="selectGym"
    :item-title="itemTitle"
  />
</template>

<script>
import GymSearchPage from "~/components/navigation/GymSearchPage.vue"
import apiLibrary from "~/store/apiLibrary.js"

export default {
  components: {
    GymSearchPage,
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
      apiLibrary.retrieveGyms(url, this.$store)
    },
    selectGym(selectedGym) {
      this.$store.commit("SET_GYM_OBJECT", selectedGym)
      this.$pushCleanedRoute(this.$router, `${selectedGym.name}/`)
    },
  },
  head() {
    return {
      title: `The Best Gyms in ${
        this.$store.state[`current_${this.itemTitle}`]
      }`,
      meta: [
        {
          hid: "description",
          name: "description",
          content: `The ${this.fetchGymList.length} Best CrossFit Gyms in ${
            this.$store.state[`current_${this.itemTitle}`]
          }. Check Out The Latest Reviews, Pricing, Contact Information for CrossFit Gyms in ${
            this.$store.state[`current_${this.itemTitle}`]
          }`,
        },
      ],
    }
  },
}
</script>
