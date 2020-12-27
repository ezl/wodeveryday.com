<template>
  <b-container fluid>
    <h1 class="text-capitalize text-center m-4">
      {{city_name}}
    </h1>
    <b-row class="w-100" align-h="center">
      <b-col :xl="2" :lg="4" :md="6" :sm="12" class="mb-4" v-for="gym in gyms.results"
             :key="gym.id">
        <b-card
          no-body
          :key="gym.id"
          :img-src="gym.photo"
          bg-variant="dark"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 20rem;"
          class="mb-2">
          <template #header>
            <h5>
              <a :href="gym.website">{{gym.name}}</a>
            </h5>
          </template>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {
    name: "GymsList",
    data() {
      return {
        gyms: {}
      }
    },

    computed: {
      countryHasStates() {
        return this.$store.getters.countries_with_countries.indexOf(this.$route.params.country) !== -1
      }
    },
    mounted() {
      this.loadGyms()
    },
    methods: {
      loadGyms() {
        let params = {
          city__iexact: this.city_name.replace(/-/gi, " "),
          country__iexact: this.$route.params["country"].replace(/-/gi, " "),
        }
        if (this.countryHasStates)
          params.full_state__iexact = this.$route.params["state"].replace(/-/gi, " ")
        this.$store.dispatch('getGymsByCity', params).then(response => {
          this.gyms = response
        })
      },
    },
    props: {
      city_name: {
        type: String,
        required: true
      }
    }
  }
</script>

<style scoped>
  h5 {
    text-align: center;
    color: var(--brand-color) !important;
  }

  h1 {
    color: var(--brand-color) !important;
  }

  h5 a {
    color: var(--brand-color) !important;
  }

  .site_button {
    background-color: var(--brand-color) !important;
    color: var(--brand-color-two);
    border: none !important;
  }

  .site_button:hover {
    background-color: var(--brand-color-two) !important;
    color: var(--brand-color);
  }

  h5 a:hover {
    text-decoration: none;
  }
</style>
