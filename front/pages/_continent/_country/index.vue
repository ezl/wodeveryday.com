<template>
  <search-card
    :item-list="stateList"
    :select-item="selectState"
    :select-subitem="selectCity"
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
      itemTitle: "country",
      stateList: {},
    }
  },
  mounted() {
    this.stateList = this.$store.state.states
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchStates()
    this.$generateBreadcrumb(this.$store, this.itemTitle)
  },
  methods: {
    fetchStates() {
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        const country = this.$store.state[`current_${this.itemTitle}`]
        let url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`
        url = encodeURI(url)

        let that = this
        this.$axios
          .$get(url)
          .then((response) => {
            that.stateList = response
          })
          .catch(function (error) {
            console.log(error)
          })
      } else {
        if (
          this.$store.state.current_state ===
          this.$store.state.constants.NOSTATE
        ) {
          this.$router.go(-1)
        } else {
          this.$store.commit(
            "SET_CURRENT_STATE",
            this.$store.state.constants.NOSTATE
          )
          this.$pushCleanedRoute(
            this.$router,
            `${this.$store.state.current_state}/`
          )
        }
      }
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$pushCleanedRoute(this.$router, `${stateName}/`)
    },
    selectCity(cityName) {
      let stateName = this.$findParent(this.stateList, cityName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$pushCleanedRoute(this.$router, `${stateName}/${cityName}/`)
    },
  },
}
</script>
