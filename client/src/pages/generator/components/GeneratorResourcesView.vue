<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore();

const {
  defaultResources,
  recources,
  activeRpdId,
} = storeToRefs(generatorViewStore)

const recources_web = ref('')
const recources_bd = ref('')

async function saveData() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "recources",
    value: {
      "web": recources_web.value,
      "bd": recources_bd.value,
    }
  })
}

watch(recources, () => {
  if (!recources.value[0]) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 0), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    recources_web.value = text
    text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 1), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    recources_bd.value = text
  } else {
    recources_web.value = recources.value[0]?.value['web']
    recources_bd.value = recources.value[0]?.value['bd']
  }
})

onBeforeMount(() => {
  if (!recources.value[0]) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 0), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    recources_web.value = text
    text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 1), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    recources_bd.value = text
  } else {
    recources_web.value = recources.value[0]?.value['web']
    recources_bd.value = recources.value[0]?.value['bd']
  }
})

</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Другие ресурсы РПД</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div class="q-pt-xs q-gutter-md">
      <q-btn
          label="Сохранить"
          color="primary"
          @click="saveData"
      />
      <q-input
          label="Ресурсы сети интернет"
          type="textarea"
          filled
          stack-label
          v-model="recources_web"
      />

      <q-input
          label="Профессиональные базы данных"
          type="textarea"
          filled
          stack-label
          v-model="recources_bd"
      />
    </div>
  </div>
</template>

<style scoped>

</style>
