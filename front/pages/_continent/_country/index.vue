<template>
  <search-card
    :is-loading="isLoading"
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
      isLoading: true,
    }
  },
  mounted() {
    this.stateList = this.$store.state.states
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
        const country = this.$retrieveStoredPathVariable(
          "country",
          this.$store,
          this.$route.params
        )
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
          this.$router.push(`${this.$store.state.current_state}/`)
        }
      }
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$router.push(`${stateName}/`)
    },
    selectCity(cityName) {
      let stateName = this.$findParent(this.stateList, cityName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${stateName}/${cityName}/`)
    },
  },
}
</script>
