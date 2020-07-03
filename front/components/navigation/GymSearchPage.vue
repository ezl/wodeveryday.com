<template>
  <v-content>
    <navbar />
    <breadcrumb />
    <v-row align="center" justify="center" style="flex-direction: column;">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-4 elevation-12 ma-4">
          <!-- eslint-disable-next-line vue/singleline-html-element-content-newline -->
          <h1 style="text-align: center;">Gyms in {{ getCityName }}</h1>
        </v-card>
      </v-col>
    </v-row>
    <v-item-group>
      <v-row justify="center" class="ma-4">
        <v-col
          v-for="(gymObject, index) in gymList"
          :key="index"
          cols="12"
          xs="12"
          sm="4"
          md="4"
          lg="3"
        >
          <v-item
            v-slot:default="{ active, toggle }"
            @change="selectItem(gymObject)"
          >
            <v-card
              class="mx-auto"
              max-width="344"
              :color="active ? 'primary' : ''"
              @click="toggle"
            >
              <nuxt-link :to="{ path: `/gym/${gymObject.name_slug}` }">
                <v-img
                  :src="gymObject.photo"
                  height="200px"
                  :alt="gymObject.name"
                />
                <v-card-title>
                  {{ gymObject.name }}
                </v-card-title>
              </nuxt-link>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-item-group>
  </v-content>
</template>

<script>
import Navbar from "~/components/global/Navbar.vue"
import Breadcrumb from "~/components/global/Breadcrumb.vue"
import _ from "lodash"

export default {
  name: "GymSearchPage",
  components: {
    Navbar,
    Breadcrumb,
  },
  props: {
    itemTitle: {
      type: String,
      required: false,
      default: undefined,
    },
    gymList: {
      type: Array,
      required: false,
      default: undefined,
    },
    selectItem: {
      type: Function,
      default: () => {},
    },
    selectSubitem: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      selectedItem: undefined,
    }
  },
  computed: {
    getCityName: function () {
      if (
        this.$store.state.constants.COUNTRIES_WITH_STATES.indexOf(
          this.$route.params["country"]
        ) === -1
      ) {
        return _.capitalize(this.$route.params["state"]).replace(/-/gi, " ")
      } else {
        return _.capitalize(this.$route.params["city"]).replace(/-/gi, " ")
      }
    },
  },
}
</script>
