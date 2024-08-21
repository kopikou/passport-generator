<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, watch} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import {useRouter} from "vue-router";
import GeneratorLeftMenu from "pages/generator/components/GeneratorLeftMenu.vue";

const generatorViewStore = useGeneratorViewStore();

const $q = useQuasar()
const router = useRouter()

const {
  cafData,
  activeRpdId,
  rpdData,
} = storeToRefs(generatorViewStore)

const props = defineProps(
  {
    id: {
      required: true
    }
  }
)

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

watch(() => props.id,
  () => {
    activeRpdId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="generator-container">
    <div class="generator-container__buttons q-pa-md">
      <q-btn
        color="secondary"
        label="Назад к списку"
        @click="router.push('/generator/')"
      />
    </div>
    <div class="text-h6 q-pa-md generator-container__header">
      <div class="text-center">
        Генератор рабочей программы дисциплины ИРНИТУ
      </div>
    </div>
    <div class="generator-container__menu">
      <div class="text-subtitle1 q-pl-md">АСУБ 2024 База данных</div>
      <generator-left-menu :id="props.id"/>
    </div>
    <div class="generator-container__content">
      <router-view/>
    </div>
  </div>
</template>

<style scoped lang="scss">

.generator-container {
  display: grid;
  grid-template-columns: 20% auto;
  grid-template-rows: auto 1fr;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  grid-template-areas:
  "a b"
  "c d";
}

.generator-container__buttons {
  grid-area: a;
}

.generator-container__header {
  grid-area: b;
}

.generator-container__menu {
  grid-area: c;
}

.generator-container__content {
  overflow-y: scroll;
  grid-area: d;
}


</style>
