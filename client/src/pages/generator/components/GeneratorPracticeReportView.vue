<script setup lang="ts">

import {ref, watchEffect} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  admissionData,
  planlinesData,
} = storeToRefs(generatorViewStore)


const documents = ref('')
const requirements = ref('')

async function saveData() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: 'practiceReport',
    value: {
      documents: documents.value,
      requirements: requirements.value,
    }
  })

  $q.notify({
    message: "Данные <span class='text-bold'>о содержании практики</span> сохранены!",
    color: "secondary",
    position: "bottom-right",
    html: true,
  })

  await generatorViewStore.getData();
  // let key = _.findKey(additionalInfo.value, x => x.type == 'practiceReport')
  // _.set(additionalInfo.value, `[${key}].value.documents`, documents.value)
  // _.set(additionalInfo.value, `[${key}].value.requirements`, requirements.value)

}

watchEffect(() => {
  documents.value = _(additionalInfo.value).filter(x => x.type == 'practiceReport').get('[0].value.documents', '')
  requirements.value = _(additionalInfo.value).filter(x => x.type == 'practiceReport').get('[0].value.requirements', '')
})

</script>

<template>
  <div class="q-px-md">
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Форма отчетности по практике</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-gutter-y-md q-mt-sm">
        <div>
          <div class="text-subtitle1">По результатам прохождения практики обучающийся должен предоставить</div>
          <ul>
            <div class="text-subtitle1 text-secondary">Документы по умолчанию список отчетных документов</div>
            <li>Дневник прохождения практики</li>
            <li>Отчет о прохождении практики</li>
            <li>Характеристика с места прохождения практики</li>
            <div v-if="admissionData?.cadmkind == 3 && planlinesData?.viewpract == 8">
              <div class="text-subtitle1 text-secondary">Пример документов для НИС</div>
              <li>Список проанализированных научных публикаций</li>
              <li>План научной работы</li>
              <li>Научную статью, подготовленную к публикации в рецензируемом научном издании, проверенную научным руководителем</li>
              <li>Результаты взаимной оценки научных статей магистрантами</li>
              <li>Презентацию результатов научной работы</li>
            </div>
          </ul>
          <q-input type="textarea" v-model="documents"
                   label="Документы подтверждающие прохождение практики" filled stack-label
                   hint="Каждый новый документ пишите с новой строчки, можно оставить пустым" @update:modelValue="saveData" :debounce="500"/>
          <div class="text-subtitle1">Требования к содержанию и оформлению отчета о прохождении практики, учитывая
            специфику направления подготовки
          </div>
          <q-input type="textarea" v-model="requirements" label="Требования к содержанию и оформлению отчета" filled
                   stack-label @update:modelValue="saveData" :debounce="500"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
