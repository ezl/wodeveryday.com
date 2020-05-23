<template>
  <search-card
    :item-list="continentObject"
    :select-item="selectContinent"
    :select-subitem="selectCountry"
  />
</template>

<script>
import SearchCard from "~/components/SearchCard.vue"

export default {
  components: {
    SearchCard,
  },
  data() {
    return {
      continentObject: {},
    }
  },
  mounted() {
    this.fetchContinents()
    this.$generateBreadcrumb(this.$store, this.$route.params)
  },
  methods: {
    fetchContinents() {
      this.continentObject = this.$store.state.continents
      if (Object.values(this.continentObject).length === 0) {
        let url = `${process.env.BACKEND_URL}/affiliates/continents`
        url = encodeURI(url)
        let that = this
        this.$axios
          .$get(url)
          .then((response) => {
            that.continentObject = response
            that.$store.commit("SET_CONTINENTS", that.continentObject)
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    selectContinent(continentName) {
      this.$store.commit("SET_CURRENT_CONTINENT", continentName)
      this.$pushCleanedRoute(this.$router, `${continentName}/`)
    },
    selectCountry(countryName) {
      let continentName = this.$findParent(this.continentObject, countryName)
      this.$store.commit("SET_CURRENT_CONTINENT", continentName)
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.$pushCleanedRoute(this.$router, `${continentName}/${countryName}/`)
      } else {
        this.$store.commit(
          "SET_CURRENT_STATE",
          this.$store.state.constants.NOSTATE
        )
        this.$pushCleanedRoute(
          this.$router,
          `${continentName}/${countryName}/${this.$store.state.constants.NOSTATE}/`
        )
      }
    },
  },
}
</script>
