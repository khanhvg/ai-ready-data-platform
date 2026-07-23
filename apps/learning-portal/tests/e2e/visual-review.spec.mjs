import { expect, test } from '@playwright/test';

test('home, architecture, and manual lab remain readable without horizontal overflow',async({page},testInfo)=>{
  for(const [name,path] of [['home','/'],['architecture','/architecture'],['lab','/labs/weighted-metrics']]){
    await page.goto(path); const dimensions=await page.evaluate(()=>({scrollWidth:document.documentElement.scrollWidth,innerWidth})); expect(dimensions,`${path} overflow`).toEqual({scrollWidth:dimensions.innerWidth,innerWidth:dimensions.innerWidth});
    await page.screenshot({path:`.artifacts/playwright/${testInfo.project.name}-${name}.png`,fullPage:true});
  }
  await expect(page.getByText('Thực hành thủ công tại local',{exact:true})).toBeVisible();
});
