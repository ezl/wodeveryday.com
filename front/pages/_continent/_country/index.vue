<template>
  <search-card
    :is-loading="isLoading"
    :item-list="stateList"
    :select-item="selectState"
    :select-subitem="selectCity"
    :back-button-enabled="true"
    :item-title="itemTitle"
    :card-title="cardTitle"
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
      cardTitle: this.$store.state.current_country,
      itemTitle: "country",
      stateList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.stateList = this.$store.state.states
    this.fetchStates()
  },
  methods: {
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
    fetchStates() {
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        const country = this.retrieveStoredPathVariable("country")
        this.isLoading = true
        let url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`
        url = encodeURI(url)

        let that = this
        this.$axios
          .$get(url)
          .then((response) => {
            that.isLoading = false
            that.stateList = response
          })
          .catch(function (error) {
            console.log(error)
            that.isLoading = false
          })
      } else {
        if (this.$store.state.current_state === "none") {
          this.$router.go(-1)
        } else {
          this.$store.commit("SET_CURRENT_STATE", "none")
          this.$router.push(`${this.$store.state.current_state}/`)
        }
      }
    },
    findParent(registryObject, name) {
      registryObject = Object.entries(registryObject)
      let parentName = registryObject.find(
        (parent) => parent[1].indexOf(name) !== -1
      )
      return parentName[0]
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$router.push(`${stateName}/`)
    },
    selectCity(cityName) {
      let stateName = this.findParent(this.stateList, cityName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${stateName}/${cityName}/`)
    },
  },
}
</script>
