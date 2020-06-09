<template>
  <v-card>
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="(link, btnName) in links"
        :key="btnName"
        color="white"
        text
        rounded
        class="my-2"
      >
        {{ btnName }}
      </v-btn>
    </v-row>
    <!-- <v-card-text> -->
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="(link, icon) in socialMediaInfo"
        :key="icon"
        class="mx-4 white--text"
        icon
      >
        <a :href="link" style="text-decoration: none;">
          <v-icon size="24px">
            {{ icon }}
          </v-icon>
        </a>
      </v-btn>
    </v-row>
    <!-- </v-card-text> -->
  </v-card>
</template>

<script>
export default {
  name: "GymFooter",
  data() {
    return {
      links: {
        "About Us": "",
        "Terms of Service": "",
        "Privacy Policy": "",
      },
      socialMediaInfo: {
        "mdi-facebook": "",
        "mdi-twitter": "",
        "mdi-linkedin": "",
        "mdi-instagram": "",
      },
    }
  },
}
</script>
