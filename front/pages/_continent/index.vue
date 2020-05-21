<template>
  <search-card
    :is-loading="isLoading"
    :item-list="countryList"
    :select-item="selectCountry"
    :select-subitem="selectCityOrState"
    :item-title="itemTitle"
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
      itemTitle: "continent",
      countryList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCountries()
    this.$generateBreadcrumb(this.$store, this.itemTitle)
  },
  methods: {
    fetchCountries() {
      const continent = this.$retrieveStoredPathVariable(
        "continent",
        this.$store,
        this.$route.params
      )
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/countries/?continent=${continent}`
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.countryList = response
          that.$store.commit("SET_COUNTRIES", that.countryList)
          that.isLoading = false
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
        })
    },
    selectCountry(countryName) {
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.$router.push(`${countryName}/`)
      } else {
        this.$store.commit(
          "SET_CURRENT_STATE",
          this.$store.state.constants.NOSTATE
        )
        this.$router.push(
          `${countryName}/${this.$store.state.constants.NOSTATE}/`
        )
      }
    },
    selectCityOrState(cityOrStateName) {
      let countryName = this.$findParent(this.countryList, cityOrStateName)
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.$store.commit("SET_CURRENT_STATE", cityOrStateName)
        this.$router.push(`${countryName}/${cityOrStateName}/`)
      } else {
        this.$store.commit("SET_CURRENT_CITY", cityOrStateName)
        this.$router.push(
          `${countryName}/${this.$store.state.constants.NOSTATE}/${cityOrStateName}/`
        )
      }
    },
  },
}
</script>
