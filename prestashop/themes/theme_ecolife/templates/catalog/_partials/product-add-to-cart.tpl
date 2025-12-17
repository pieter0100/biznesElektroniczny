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
<div class="product-add-to-cart js-product-add-to-cart">
  {if !$configuration.is_catalog}
    <span class="control-label">{l s='Quantity' d='Shop.Theme.Catalog'}</span>

    {block name='product_quantity'}
      {* 1. KONTENER ILOŚCI I PRZYCISKU *}
      <div class="product-quantity clearfix" style="display: flex; flex-wrap: wrap; align-items: center;">
        
        <div class="qty" style="margin-bottom: 15px; margin-right: 10px;">
          <input
            type="number"
            name="qty"
            id="quantity_wanted"
            inputmode="numeric"
            pattern="[0-9]*"
            {if $product.quantity_wanted}
              value="{$product.quantity_wanted}"
              min="{$product.minimal_quantity}"
            {else}
              value="1"
              min="1"
            {/if}
            class="input-group"
            style="height: 45px; width: 65px; text-align: center; border: 1px solid #ddd; border-radius: 4px;"
          >
        </div>

        <div class="add" style="width: 100%; order: 2; margin-bottom: 10px;">
          <button
            class="btn btn-primary add-to-cart"
            data-button-action="add-to-cart"
            type="submit"
            {if !$product.add_to_cart_url}disabled{/if}
            style="width: 100%; background-color: #e23b1a; color: white; border: none; height: 55px; font-weight: bold; text-transform: uppercase; font-size: 18px; border-radius: 4px;"
          >
            {l s='Add to cart' d='Shop.Theme.Actions'}
          </button>
        </div>

        <div style="display: none !important;">
          {hook h='displayAfterButtonCart'}
          {hook h='displayProductActions' product=$product}
        </div>
      </div> {* KONIEC div product-quantity *}

      {* 2. NOWA SEKCJA POD PRZYCISKIEM (POZA FLEXEM) *}
      <div class="product-features-mini" style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px; clear: both;">
        <div class="product-rating-line" style="margin-bottom: 10px; display: flex; align-items: center;">
            <span style="margin-right: 10px;">Ocena:</span>
            <div class="stars" style="color: #ccc;">
                <i class="material-icons">star_border</i>
                <i class="material-icons">star_border</i>
                <i class="material-icons">star_border</i>
                <i class="material-icons">star_border</i>
                <i class="material-icons">star_border</i>
            </div>
        </div>

        <div class="product-meta-data" style="display: flex; gap: 40px; margin-bottom: 20px;">
            <div>
                <span style="color: #666; font-size: 13px;">Producent:</span><br>
                <strong>
                    {if isset($product.id_manufacturer) && $product.id_manufacturer > 0}
                        {$product.manufacturer_name}
                    {else}
                        Nieokreślony
                    {/if}
                </strong>
            </div>
            <div>
                <span style="color: #666; font-size: 13px;">Kod produktu:</span><br>
                <strong>{$product.reference}</strong>
            </div>
        </div>

        <div class="product-actions-links" style="list-style: none; padding: 0; font-size: 14px; border-top: 1px solid #eee; padding-top: 15px;">
            <div style="margin-bottom: 8px; display: flex; align-items: center;">
                <i class="material-icons" style="margin-right: 8px; font-size: 18px;">mail_outline</i>
                <a href="#" style="text-decoration: underline; color: #333;">zapytaj o produkt</a>
            </div>
            <div style="margin-bottom: 8px; display: flex; align-items: center;">
                <i class="material-icons" style="margin-right: 8px; font-size: 18px;">favorite_border</i>
                <a href="#" style="text-decoration: underline; color: #333;">poleć znajomemu</a>
            </div>
            <div style="margin-bottom: 8px; display: flex; align-items: center;">
                <i class="material-icons" style="margin-right: 8px; font-size: 18px;">chat_bubble_outline</i>
                <a href="#" style="text-decoration: underline; color: #333;">dodaj opinię</a>
            </div>
        </div>
      </div>
    {/block}

    {block name='product_availability'}
      <span id="product-availability" class="js-product-availability">
        {if $product.show_availability && $product.availability_message}
          {if $product.availability == 'available'}
            <i class="material-icons rtl-no-flip product-available">&#xE5CA;</i>
          {elseif $product.availability == 'last_remaining_items'}
            <i class="material-icons product-last-items">&#xE002;</i>
          {else}
            <i class="material-icons product-unavailable">&#xE14B;</i>
          {/if}
          {$product.availability_message}
        {/if}
      </span>
    {/block}

    {block name='product_minimal_quantity'}
      <p class="product-minimal-quantity js-product-minimal-quantity">
        {if $product.minimal_quantity > 1}
          {l
          s='The minimum purchase order quantity for the product is %quantity%.'
          d='Shop.Theme.Checkout'
          sprintf=['%quantity%' => $product.minimal_quantity]
          }
        {/if}
      </p>
    {/block}
  {/if}
</div>