<template>
  <div id="page_container">
    <v-card-text id="search_bar">
      <v-autocomplete
        v-model="selectedGym"
        item-text="name"
        :items="affiliateList"
        :loading="isLoading"
        color="white"
        hide-no-data
        hide-selected
        label="Affiliate Search"
        placeholder="Start typing to Search"
        prepend-icon="mdi-dumbbell"
        return-object
        @change="selectGym()"
      />
    </v-card-text>
  </div>
</template>

<script>
export default {
  data() {
    return {
      affiliateList: [],
      isLoading: true,
      selectedGym: undefined,
    }
  },
  mounted() {
    console.log(process.env.GCP_API_KEY)
    this.fetchAffiliates()
  },
  methods: {
    fetchAffiliates() {
      let url = `${process.env.BACKEND_URL}/affiliates/`
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
    selectGym() {
      this.$store.commit("SET_CURRENT_AFFILIATE", this.selectedGym)
      this.$router.replace(
        "gyms/" +
          this.selectedGym.city +
          "/" +
          this.selectedGym.name.replace(/ /g, "_")
      )
    },
  },
}
</script>

<style lang="scss" scoped>
#search_bar {
  width: 50%;
  background-color: rgba(0, 0, 0, 0.75);
  min-width: 450px;
}
#page_container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url("https://images.unsplash.com/photo-1534367610401-9f5ed68180aa?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}
</style>
