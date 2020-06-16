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
import _ from "lodash"

export default {
  components: {
    GymSearchPage,
  },
  async asyncData({ route, store }) {
    const country = route.params["country"]
    const state = route.params["state"]
    const city = route.params["city"]
    let url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`
    if (state != store.state.constants.NOSTATE)
      url += `&full_state__iexact=${state}`
    url = encodeURI(url)

    const gymList = await apiLibrary.retrieveGyms(url, store)
    return {
      gymList,
    }
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
    fetchCityName: function () {
      return _.capitalize(this.$route.params[this.itemTitle]).replace(
        /-/gi,
        " "
      )
    },
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        this.fetchCityName
      )
    },
    fetchPageDescription: function () {
      return `The ${this.gymList.length} Best CrossFit Gyms in ${this.fetchCityName}. Check Out The Latest Reviews, Pricing, Contact Information for CrossFit Gyms in ${this.fetchCityName}`
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
      title: this.fetchPageTitle,
      meta: [
        {
          hid: "description",
          name: "description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:title",
          content: this.fetchPageTitle,
        },
        {
          property: "og:description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:image",
          content: this.$store.state.constants.DEFAULT_GYM_THUMBNAIL,
        },
      ],
    }
  },
}
</script>
