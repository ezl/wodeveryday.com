<template>
  <v-card>
    <v-tabs v-model="currentNavTab" dark show-arrows centered>
      <v-tabs-slider />
      <v-tab
        v-for="(tab, index) in navbarTabs"
        :key="index"
        :disabled="index == 2"
      >
        <h1 v-if="index == 2" style="color: white; opacity: 1;">
          {{ tab }}
        </h1>
        <span v-if="index != 2">{{ tab }}</span>
      </v-tab>
    </v-tabs>
  </v-card>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      currentNavTab: 0,
      navbarTabs: ["Find A Gym", "About", "WOD EVERY DAY", "Contact", "Blog"],
    }
  },
}
</script>
