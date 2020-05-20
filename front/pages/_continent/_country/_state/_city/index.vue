<template>
  <gym-search-card
    :is-loading="isLoading"
    :gym-list="affiliateList"
    :select-item="selectAffiliate"
    :item-key="'name'"
    :back-button-enabled="true"
    :item-title="itemTitle"
    :card-title="cardTitle"
  />
</template>

<script>
import GymSearchCard from "~/components/GymSearchCard.vue"

export default {
  components: {
    GymSearchCard,
  },
  data() {
    return {
      cardTitle: this.$store.state.current_city,
      itemTitle: "city",
      affiliateList: [],
      isLoading: false,
    }
  },
  mounted() {
    this.fetchAffiliates()
    this.generateBreadcrumb()
  },
  methods: {
    generateBreadcrumb() {
      let pages = ["continent", "country", "state", "city"]
      let currentPage = pages.indexOf(this.itemTitle || "")
      if (currentPage != -1) {
        let breadcrumbNames = ["Home"]
        for (let i = 0; i <= currentPage; i++) {
          let name = this.$store.state["current_" + pages[i]]
          if (name != "none") breadcrumbNames.push(name)
        }
        this.$store.commit("SET_GLOBAL_BREADCRUMB_NAMES", breadcrumbNames)
      } else {
        this.$store.commit("SET_GLOBAL_BREADCRUMB_NAMES", [])
      }
    },
    retrieveStoredPathVariable(pathVarName) {
      let pathVariable = this.$store.state[`current_${pathVarName}`]
      if (pathVariable === undefined) {
        pathVariable = this.$route.params[pathVarName]
        this.$store.commit(
          `SET_CURRENT_${pathVarName.toUpperCase()}`,
          pathVariable
        )
      }
      return pathVariable
    },
    fetchAffiliates() {
      const country = this.retrieveStoredPathVariable("country")
      const state = this.retrieveStoredPathVariable("state")
      const city = this.retrieveStoredPathVariable("city")
      let url = `${process.env.BACKEND_URL}/affiliates/?city=${city}&country=${country}`
      if (state != "none") url += `&state=${state}`
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.affiliateList = response.results
          that.isLoading = false
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
        })
    },
    getStateOrCountry() {
      let currentState = this.$store.state.current_state
      if (currentState) {
        return `${this.$store.state.current_country}/${currentState}`
      } else {
        return `${this.$store.state.current_country}/none`
      }
    },
    selectAffiliate(selectedAffiliate) {
      this.$store.commit("SET_CURRENT_AFFILIATE", selectedAffiliate)
      this.$router.push(`${selectedAffiliate.name}/`)
    },
  },
}
</script>
