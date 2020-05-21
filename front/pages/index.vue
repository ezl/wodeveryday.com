<template>
  <search-card
    :is-loading="isLoading"
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
      isLoading: true,
    }
  },
  mounted() {
    this.fetchContinents()
    this.$generateBreadcrumb(this.$store)
  },
  methods: {
    fetchContinents() {
      this.continentObject = this.$store.state.continents
      if (Object.values(this.continentObject).length === 0) {
        this.isLoading = true
        let url = `${process.env.BACKEND_URL}/affiliates/continents`
        url = encodeURI(url)
        let that = this
        this.$axios
          .$get(url)
          .then((response) => {
            that.continentObject = response
            that.$store.commit("SET_CONTINENTS", that.continentObject)
            that.isLoading = false
          })
          .catch(function (error) {
            console.log(error)
            that.isLoading = false
          })
      } else {
        this.isLoading = false
      }
    },
    selectContinent(continentName) {
      this.$store.commit("SET_CURRENT_CONTINENT", continentName)
      this.$router.push(`${continentName}/`)
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
        this.$router.push(`${continentName}/${countryName}/`)
      } else {
        this.$store.commit("SET_CURRENT_STATE", "none")
        this.$router.push(`${continentName}/${countryName}/none/`)
      }
    },
  },
}
</script>
