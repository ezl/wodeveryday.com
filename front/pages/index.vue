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
    this.generateBreadcrumb()
  },
  methods: {
    generateBreadcrumb() {
      let pages = ["continent", "country", "state", "gym"]
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
    findParent(registryObject, name) {
      registryObject = Object.entries(registryObject)
      let parentName = registryObject.find(
        (parent) => parent[1].indexOf(name) !== -1
      )
      return parentName[0]
    },
    selectCountry(countryName) {
      let continentName = this.findParent(this.continentObject, countryName)
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
