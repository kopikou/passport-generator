<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore();

const {
  defaultResources,
  resources,
  activeRpdId,
  additionalInfo,
} = storeToRefs(generatorViewStore)

const resources_web = ref('')
const resources_bd = ref('')

async function saveData() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "resources",
    value: {
      "web": resources_web.value,
      "bd": resources_bd.value,
    }
  })
  let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  if (key === undefined) {
    additionalInfo.value.push(r.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value`, r.data.value)
  }
}

watch(resources, () => {
  if (!resources.value[0]?.value['web']) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 0), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    resources_web.value = text
    text = ''
  } else {
    resources_web.value = resources.value[0]?.value['web']
  }
  if (!resources.value[0]?.value['bd']) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 1), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    resources_bd.value = text
  } else {
    resources_bd.value = resources.value[0]?.value['bd']
  }
})

onBeforeMount(() => {
  if (!resources.value[0]?.value['web']) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 0), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    resources_web.value = text
    text = ''
  } else {
    resources_web.value = resources.value[0]?.value['web']
  }
  if (!resources.value[0]?.value['bd']) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 1), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    resources_bd.value = text
  } else {
    resources_bd.value = resources.value[0]?.value['bd']
  }
})

</script>

<template>
  <div style="width: 95%">
    <span class="text-h6 q-pl-lg">Другие ресурсы используемые по дисциплине</span>
    <p>бла бла бла</p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div class="q-pt-xs q-gutter-md">

      <q-input
        label="Ресурсы сети интернет"
        type="textarea"
        filled
        stack-label
        v-model="resources_web"
      />

      <q-input
        label="Профессиональные базы данных"
        type="textarea"
        filled
        stack-label
        v-model="resources_bd"
      />
      <q-btn
        label="Сохранить"
        color="primary"
        @click="saveData"
      />
    </div>
  </div>
</template>

<style scoped>

</style>
