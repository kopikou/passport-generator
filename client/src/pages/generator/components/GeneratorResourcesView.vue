<script setup lang="ts">

import {nextTick, onBeforeMount, ref, watch} from "vue";
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
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  // $q.loading.show({message: "Сохранение данных"})
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "resources",
    value: {
      "web": resources_web.value,
      "bd": resources_bd.value,
    }
  })

  await generatorViewStore.getData();

  $q.notify({
    message: "Данные <span class='text-bold'>об используемых ресурсах</span> сохранены!",
    color: "secondary",
    position: "bottom-right",
    html: true,
  })
  generatorViewStore.checkErrors()

  // if (r.status == 200) {
  //   let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  //   if (key === undefined) {
  //     additionalInfo.value.push(r.data)
  //   } else {
  //     _.set(additionalInfo.value, `[${key}].value`, r.data.value)
  //   }
  //   generatorViewStore.checkErrors()
  // } else {
  //   $q.notify({
  //     message: "Данные <span class='text-bold'>об используемых ресурсах</span> не сохранены!",
  //     color: "negative",
  //     position: "bottom",
  //     html: true,
  //   })
  // }
  // $q.loading.hide()
}

watch(resources, () => {
  if (!resources.value[0]?.value['web']) {
    let text = ''
    _.forEach(_.filter(defaultResources.value, (x) => x.type == 0), (value, key) => {
      text += key + 1 + '. ' + value['url'] + '\n'
    })
    resources_web.value = text
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
  if (resources_bd.value && resources_web.value) {
    if (!resources.value[0]?.value['web'] || !resources.value[0]?.value['bd']) {
      saveData()
    }
  }
}, {immediate: true})


</script>

<template>
  <div class="q-px-md">
    <span class="text-h6">Другие ресурсы используемые по дисциплине</span>
    <p></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <div class="q-pt-xs q-gutter-md">
      <div class="text-h6">Используемые ресурсы сети "Интернет"</div>
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
