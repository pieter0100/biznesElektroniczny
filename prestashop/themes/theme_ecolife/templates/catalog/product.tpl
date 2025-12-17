{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
{extends file=$layout}

{block name='head_seo' prepend}
  <link rel="canonical" href="{$product.canonical_url}">
{/block}

{block name='head' append}
  <meta property="og:type" content="product">
  <meta property="og:url" content="{$urls.current_url}">
  <meta property="og:title" content="{$page.meta.title}">
  <meta property="og:site_name" content="{$shop.name}">
  <meta property="og:description" content="{$page.meta.description}">
  <meta property="og:image" content="{$product.cover.large.url}">
  {if $product.show_price}
    <meta property="product:pretax_price:amount" content="{$product.price_tax_exc}">
    <meta property="product:pretax_price:currency" content="{$currency.iso_code}">
    <meta property="product:price:amount" content="{$product.price_amount}">
    <meta property="product:price:currency" content="{$currency.iso_code}">
  {/if}
  {if isset($product.weight) && ($product.weight != 0)}
  <meta property="product:weight:value" content="{$product.weight}">
  <meta property="product:weight:units" content="{$product.weight_unit}">
  {/if}
{/block}

{block name='content'}

  <section id="main" itemscope itemtype="https://schema.org/Product">
    <meta itemprop="url" content="{$product.url}">

    {if $postheme.productp_layout == '1'}
      {include file="catalog/product_layouts/product_layout1.tpl"}
    {elseif $postheme.productp_layout == '2'}
      {include file="catalog/product_layouts/product_layout2.tpl"}
    {elseif $postheme.productp_layout == '3'}
      {include file="catalog/product_layouts/product_layout3.tpl"}
    {elseif $postheme.productp_layout == '4'}
      {include file="catalog/product_layouts/product_layout4.tpl"}
    {/if}

    {block name='product_images_modal'}
      {include file='catalog/_partials/product-images-modal.tpl'}
    {/block}

    {block name='page_footer_container'}
      <footer class="page-footer">
        {block name='page_footer'}
          <!-- Footer content -->
        {/block}
      </footer>
    {/block}
  </section>

{/block}


<div class="row product-container product-layout1">
  <div class="col-md-6">
    {block name='page_content_container'}
      <section class="page-content" id="content">
        {block name='page_content'}
          {block name='product_cover_thumbnails'}
              {include file='catalog/_partials/product-cover-thumbnails.tpl'}
          {/block}
        {/block}
      </section>
    {/block}
    </div>
    <div class="col-md-6">
		{block name='page_header_container'}
		{block name='page_header'}
		<h1 class="h1 namne_details" >{block name='page_title'}{$product.name}{/block}</h1>
		{/block}
		{/block}
		{hook h="displayReviewsProduct"}
		{block name='product_prices'}
		{include file='catalog/_partials/product-prices.tpl'}
		{/block}

		<div class="product-information">
			 {block name='product_description_short'}
			  <div id="product-description-short-{$product.id}" class="product-description" >{$product.description_short nofilter}</div>
			{/block}

			{if $product.is_customizable && count($product.customizations.fields)}
			  {block name='product_customization'}
				{include file="catalog/_partials/product-customization.tpl" customizations=$product.customizations}
			  {/block}
			{/if}

			<div class="product-actions">
				{block name='product_buy'}
				<form action="{$urls.pages.cart}" method="post" id="add-to-cart-or-refresh">
				  <input type="hidden" name="token" value="{$static_token}">
				  <input type="hidden" name="id_product" value="{$product.id}" id="product_page_product_id">
				  <input type="hidden" name="id_customization" value="{$product.id_customization}" id="product_customization_id">
				  {block name='product_variants'}
					{include file='catalog/_partials/product-variants.tpl'}
				  {/block}
				  {hook h='displaySizeChart'}	
				  {block name='product_pack'}
					{if $packItems}
					  <section class="product-pack">
						<p class="h4">{l s='This pack contains' d='Shop.Theme.Catalog'}</p>
						{foreach from=$packItems item="product_pack"}
						  {block name='product_miniature'}
							{include file='catalog/_partials/miniatures/pack-product.tpl' product=$product_pack showPackProductsPrice=$product.show_price}
						  {/block}
						{/foreach}
					</section>
					{/if}
				  {/block}

				  {block name='product_discounts'}
					{include file='catalog/_partials/product-discounts.tpl'}
				  {/block}

				  {block name='product_add_to_cart'}
					{include file='catalog/_partials/product-add-to-cart.tpl'}
				  {/block}

				  {block name='product_additional_info'}
					{include file='catalog/_partials/product-additional-info.tpl'}
				  {/block}

				  {* Input to refresh product HTML removed, block kept for compatibility with themes *}
				  {block name='product_refresh'}{/block}
				</form>
			  {/block}

			</div>

			{block name='hook_display_reassurance'}
			  {hook h='displayReassurance'}
			{/block}

		</div>
    </div>
	<div class="col-md-12">
		{block name='product_tabs'}
		  <div class="product-tabs-container" style="margin-top: 50px;">
			<ul class="nav nav-tabs" id="productTabs" role="tablist" style="display: flex; border-bottom: 1px solid #ddd; list-style: none; padding: 0;">
				
				{* 1. Produkty w zestawie - tylko jeśli to jest zestaw *}
				{if $product.pack_items|count > 0}
				<li class="nav-item">
					<a class="nav-link" data-toggle="tab" href="#pack-items" role="tab" style="padding: 10px 25px; text-transform: uppercase; font-weight: bold; color: #333; text-decoration: none; display: block;">
					{l s='Produkty w zestawie' d='Shop.Theme.Catalog'}
					</a>
				</li>
				{/if}

				{* 2. Opis *}
				<li class="nav-item">
				<a class="nav-link active" data-toggle="tab" href="#description" role="tab" style="padding: 10px 25px; text-transform: uppercase; font-weight: bold; color: #333; text-decoration: none; display: block;">
					{l s='Opis' d='Shop.Theme.Catalog'}
				</a>
				</li>

				{* 3. Koszty dostawy (statyczna zakładka lub hak) *}
				<li class="nav-item">
				<a class="nav-link" data-toggle="tab" href="#shipping-costs" role="tab" style="padding: 10px 25px; text-transform: uppercase; font-weight: bold; color: #333; text-decoration: none; display: block;">
					{l s='Koszty dostawy' d='Shop.Theme.Catalog'}
				</a>
				</li>

				{* 4. Opinie *}
				<li class="nav-item">
				<a class="nav-link" data-toggle="tab" href="#reviews" role="tab" style="padding: 10px 25px; text-transform: uppercase; font-weight: bold; color: #333; text-decoration: none; display: block;">
					{l s='Opinie o produkcie' d='Shop.Theme.Catalog'} (0)
				</a>
				</li>
			</ul>

			<div class="tab-content" id="productTabsContent" style="padding: 30px; border: 1px solid #ddd; border-top: none; background: #fff;">
				
				{if $product.pack_items|count > 0}
				<div class="tab-pane fade" id="pack-items" role="tabpanel">
					{include file='catalog/_partials/product-pack.tpl' pack_items=$product.pack_items}
				</div>
				{/if}

				<div class="tab-pane fade show active" id="description" role="tabpanel">
				{block name='product_description'}
					<div class="product-description">{$product.description nofilter}</div>
				{/block}
				</div>

				<div class="tab-pane fade" id="shipping-costs" role="tabpanel">
					<div class="delivery-table-container">
						<table class="table" style="width: 100%; border-collapse: collapse;">
						<tbody>
							<tr style="border-bottom: 1px solid #ebebeb;">
							<td style="padding: 15px 0; color: #666;">Paczkomaty (przelew)</td>
							<td style="padding: 15px 0; text-align: right; font-weight: bold;">14,90 zł</td>
							</tr>
							<tr style="border-bottom: 1px solid #ebebeb;">
							<td style="padding: 15px 0; color: #666;">Kurier (przelew)</td>
							<td style="padding: 15px 0; text-align: right; font-weight: bold;">18,00 zł</td>
							</tr>
							<tr style="border-bottom: 1px solid #ebebeb;">
							<td style="padding: 15px 0; color: #666;">Kurier (pobranie)</td>
							<td style="padding: 15px 0; text-align: right; font-weight: bold;">20,00 zł</td>
							</tr>
							<tr style="border-bottom: 1px solid #ebebeb;">
							<td style="padding: 15px 0; color: #666;">
								Odbiór osobisty z Centrum Domowych Alkoholi<br>
								<span style="font-size: 12px;">(ul. Kołowa 46, 03-536 Warszawa)</span>
							</td>
							<td style="padding: 15px 0; text-align: right; font-weight: bold;">0,00 zł</td>
							</tr>
							<tr>
							<td style="padding: 15px 0; color: #666;">
								Odbiór osobisty z magazynu Firma ARES<br>
								<span style="font-size: 12px;">(ul. Cieślewskich 37Z, 03-017 Warszawa)</span>
							</td>
							<td style="padding: 15px 0; text-align: right; font-weight: bold;">0,00 zł</td>
							</tr>
						</tbody>
						</table>
					</div>
				</div>

				<div class="tab-pane fade" id="reviews" role="tabpanel">
				{hook h='displayProductComments' product=$product}
				</div>
			</div>
			</div>
		{/block}
	</div>
</div>