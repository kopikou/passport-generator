<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";
import {useQuasar} from "quasar";

const generatorViewStore = useGeneratorViewStore();

const {
  defaultResources,
  resources,
  activeRpdId,
  additionalInfo,
  disabled,
} = storeToRefs(generatorViewStore)

const resources_web = ref('')
const resources_bd = ref('')

const $q = useQuasar()

async function saveData() {
  $q.loading.show({message: "Сохранение данных"})
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "resources",
    value: {
      "web": resources_web.value,
      "bd": resources_bd.value,
    }
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>об используемых ресурсах</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
  let key = _.findKey(additionalInfo.value, (x) => x.id == v.data.id)
  if (key === undefined) {
    additionalInfo.value.push(v.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value`, v.data.value)
  }
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>об используемых ресурсах</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })
  $q.loading.hide()
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
      <div class="text-h6">Используемые ресурсы сети интернет</div>
      <q-input
        label="Ресурсы сети интернет"
        type="textarea"
        filled
        stack-label
        v-model="resources_web"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />

      <div class="text-h6">Используемые профессиональные базы данных</div>
      <q-input
        label="Профессиональные базы данных"
        type="textarea"
        filled
        stack-label
        v-model="resources_bd"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
<!--      <q-btn-->
<!--        label="Сохранить"-->
<!--        color="primary"-->
<!--        @click="saveData"-->
<!--        v-show="!disabled"-->
<!--      />-->
    </div>
  </div>
</template>

<style scoped>

</style>
